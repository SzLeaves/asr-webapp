import os
import pickle

import tensorflow as tf
from ppasr.infer_utils.pun_predictor import PunctuationPredictor

from asrlab.settings import ASR_MODEL_PATH, PUN_MODEL_PATH
from asrlab.settings import DATA_WEIGHT_PATH, DICT_PATH
from asrlab.settings import logger

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
load_model = tf.keras.models.load_model

ASR_MODEL = None
PUN_MODEL = None
DATA_WEIGHT = dict()


def loadData():
    global ASR_MODEL
    global PUN_MODEL
    global DATA_WEIGHT

    # 加载数据
    # 读取音频模型均值, 标准差
    with open(DATA_WEIGHT_PATH, "rb") as file:
        mfcc_mean, mfcc_std = pickle.load(file)
        DATA_WEIGHT['mfcc_mean'] = mfcc_mean
        DATA_WEIGHT['mfcc_std'] = mfcc_std
        logger.info("权重数据加载成功")

    # 读取词库
    with open(DICT_PATH, "rb") as file:
        _, id2char = pickle.load(file)
        del _
        DATA_WEIGHT['id2char'] = id2char
        logger.info("词库数据加载成功")

    # 加载语音识别模型
    ASR_MODEL = load_model(ASR_MODEL_PATH, compile=False)
    logger.info("语音识别模型加载成功")
    logger.info("Tensorflow version: " + tf.__version__)

    # 加载标点符号预测模型
    PUN_MODEL = PunctuationPredictor(model_dir=PUN_MODEL_PATH, use_gpu=False)
