import time
import asyncio

from logging import getLogger

from aiokafka import AIOKafkaProducer

from storage.models import SRProduct

logger = getLogger('app.producer')


async def produce():

    logger.info('Start publishing')
    topic = 'products'
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: str(v).encode('utf-8')
    )

    async def publish(product_id):
        await producer.send_and_wait(topic, value=product_id)
        logger.info(f'send {product_id}')

    await producer.start()

    try:
        start_time = time.time()

        product_ids = await SRProduct.get_ids_list()
        await asyncio.gather(*map(publish, product_ids))
        logger.info(f'Publishing {len(product_ids)} messages completed '
                    f'in {(time.time() - start_time):.2f} seconds')
    except Exception as e:
        logger.exception(
            msg=f'Unexpected error: {e}',
            exc_info=True
        )
    finally:
        await producer.stop()
        logger.info('No more message to publish. Stopping producer.')
        return


if __name__ == '__main__':
    asyncio.run(produce())
