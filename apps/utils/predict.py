from functools import reduce

import librosa
import librosa.feature
import numpy as np
import tensorflow as tf

from utils.loader import ASR_MODEL, PUN_MODEL, DATA_WEIGHT

ctc_decode, get_value = (
    tf.keras.backend.ctc_decode,
    tf.keras.backend.get_value,
)


def loadMfcc(filePath, mfccValue, sampleRate=16000):
    # 读取文件
    data, sr = librosa.load(path=filePath, sr=sampleRate)

    # 去除音频中所有的空白静默部分
    y_split = librosa.effects.split(data, top_db=23)
    y_split = np.array(list(reduce(lambda x, y: np.concatenate((x, y)),
                                   [data[x[0]: x[1]] for x in y_split])))

    # 预加重
    y_split = librosa.effects.preemphasis(y_split, coef=0.97)

    # 提取MFCC特征
    y_mfcc = librosa.feature.mfcc(y=y_split, sr=sampleRate,
                                  n_mfcc=mfccValue, n_fft=512, lifter=22,
                                  hop_length=int(sampleRate * 0.01),
                                  win_length=int(sampleRate * 0.025))
    # 特征矩阵转置
    y_mfcc = y_mfcc.transpose()
    # 标准化
    y_mfcc = (y_mfcc - DATA_WEIGHT['mfcc_mean']) / (DATA_WEIGHT['mfcc_std'] + 1e-14)

    return y_mfcc


def decodeAndPredict(filePath):
    # 语音识别模型预测文本 (expand_dims用于增加维度匹配模型输入)
    feature = loadMfcc(filePath, mfccValue=32)
    pred = ASR_MODEL.predict(np.expand_dims(feature, axis=0))

    # 音频帧数
    input_length = np.array((feature.shape[1],))

    # 解码
    decode_res = ctc_decode(pred, input_length, greedy=True)
    # 获取预测的序列数组, 筛选有效值 (> -1)
    pred_index = get_value(decode_res[0][0])
    pred_index = [item for item in pred_index[0] if item > -1]

    # 使用词库将预测标号转换为文本
    pred_text = ""
    for index in pred_index:
        pred_text += DATA_WEIGHT['id2char'][index]

    # 预测文本标点符号
    pred_text = PUN_MODEL(pred_text)

    # 返回处理结果
    return pred_text
