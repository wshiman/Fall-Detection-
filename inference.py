import os
import argparse
from humanomni import model_init, mm_infer
from humanomni.utils import disable_torch_init
from transformers import BertTokenizer
import time
# 设置环境变量
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def main():
    parser = argparse.ArgumentParser(description="HumanOmni Inference Script")
    # parser.add_argument('--modal', type=str, default='video_audio', help='Modal type (video or video_audio)')
    
    modal= 'video'
    # parser.add_argument('--model_path', type=str, required=True, help='Path to the model')
    model_path='/data/data2/shiman/R1-Omni/humanomni-0.5B'
    # parser.add_argument('--video_path', type=str, required=True, help='Path to the video file')
    # video_path = '/data/data2/shiman/R1-Omni/123test.mp4'
    # parser.add_argument('--instruct', type=str, required=True, help='Instruction for the model')
    instruct = 'As an emotional recognition expert; throughout the video, which emotion conveyed by the characters is the most obvious to you?  Output the thinking process in <think> </think> and final emotion in <answer> </answer> tags.'
    # instruct = 'describe the video in detail'
    # instruct = 'User: As an action recognition expert; throughout the video, which action conveyed by the characters is the most obvious to you?  Output the thinking process in <think> </think> and final action in <answer> </answer> tags.'
    args = parser.parse_args()

    # 初始化BERT分词器
    bert_model = "/data/data2/shiman/R1-Omni/bert-base-uncased"
    bert_tokenizer = BertTokenizer.from_pretrained(bert_model)

    # 禁用Torch初始化
    disable_torch_init()

    # 初始化模型、处理器和分词器
    # model, processor, tokenizer = model_init(args.model_path)
    model, processor, tokenizer = model_init(model_path)

 

    # 处理视频输入
    count = 0
    video_dir = '/data/data2/shiman/dataset/onlyone'
    for video_path in os.listdir(video_dir):
        count+=1
        print(count)
        if video_path.endswith(".mp4"):
            action_category = os.path.splitext(video_path)[0]
            print(f'action is {action_category}')
            video_tensor = processor['video'](os.path.join(video_dir,video_path))
    
            # 根据modal类型决定是否处理音频
            if modal == 'video_audio' or modal == 'audio':
                audio = processor['audio'](video_path)[0]
            else:
                audio = None

            audio = None
            # 执行推理
            # import ipdb; ipdb.set_trace()
            start_time=time.time()
            output = mm_infer(video_tensor, instruct, model=model, tokenizer=tokenizer, modal=modal, question=instruct, bert_tokeni=bert_tokenizer, do_sample=False, audio=audio)
            print(output)
            print(f'processing {action_category} time is {time.time()-start_time}')

if __name__ == "__main__":
    main()
