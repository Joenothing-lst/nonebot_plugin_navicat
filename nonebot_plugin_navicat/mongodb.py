# -*- coding: utf-8 -*-
"""
对外导出mongodb连接
"""
import nonebot

try:
    from motor import motor_asyncio
except ImportError:
    motor_asyncio = None

driver: nonebot.Driver = nonebot.get_driver()
config: nonebot.config.Config = driver.config

mongodb_opened: bool = False


@driver.on_startup
async def connect_to_mongodb():
    global mongodb_opened
    if config.mongodb_host is not None:
        nonebot.require("nonebot_plugin_navicat").mongodb_client = motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{config.mongodb_user}:{config.mongodb_password}@{config.mongodb_host}:{config.mongodb_port}")
        mongodb_opened = True
        nonebot.logger.info("connect to mongodb")


@driver.on_shutdown
async def free_db():
    global mongodb_opened
    if mongodb_opened:
        mongodb_client: motor_asyncio.AsyncIOMotorClient = nonebot.require("nonebot_plugin_navicat").mongodb_client
        mongodb_client.close()
        mongodb_opened = False
        nonebot.logger.info("disconnect to mongodb")
