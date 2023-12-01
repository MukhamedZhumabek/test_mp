import time
import asyncio

from logging import getLogger

from aiokafka import AIOKafkaConsumer

from storage.models import SRProduct

logger = getLogger('app.consumer')


async def consume():

    async def handle(products):
        logger.info(type(products))
        logger.info(products[0])
        logger.info(products[1])
        try:
            errors = await SRProduct.bulk_update_processed_time(products)
            if errors:
                logger.error(f'Can not handle products {errors}')
        except Exception as e:
            logger.exception(
                msg=f'Unexpected error: {e}',
                exc_info=True
            )

    logger.info('Try to connect kafka topic')

    consumer = AIOKafkaConsumer(
        'products',
        bootstrap_servers='kafka:9092',
        group_id='products',
        auto_offset_reset='earliest',
        value_deserializer=lambda v: v.decode('utf-8')
    )

    await consumer.start()
    logger.info('Connected. Search new messages')
    messages = await consumer.getmany(timeout_ms=1000)

    if not messages:
        await consumer.stop()
        logger.info('No messages in the queue. Stopping consumer.')
        return

    try:
        start_time = time.time()
        count = 0
        for partition, partition_messages in messages.items():
            count += len(partition_messages)
            await handle([int(msg.value) for msg in partition_messages])
        logger.info(f'Handling {count} messages completed in {(time.time() - start_time):.2f} seconds')

    finally:
        await consumer.stop()
        logger.info('No more messages in queue. Stopping consumer.')
        return


if __name__ == '__main__':
    asyncio.run(consume())
