# Build Up!

​	本分支的主要工作在于构建“手势识别”模块, 想要运行此模块，请自行创建一个干净的虚拟环境，并且使用如下在该虚拟环境中输入如下的指令：

```
pip install mediapipe -i https://pypi.tuna.tsinghua.edu.cn/simple
```

​	这里任何源都可以，只要目标的维护源有mediapipe(笑)

​	等待稍后片刻，就可以运行test.py了(建议先阅读这个文件后再进行运行)

# Branch Structure Reference

```
.
├── buildup.md
├── debug_action.py			# debug模块
├── gesture_recognitions.py	# 手势识别逻辑核心
├── hands_capture.py		# 手势关键点捕捉
├── image_factory.py		# mediapipe.Image, file_path_referred_image, cv2.Mat转换核心
├── models
│   ├── default
│   │   └── default_gesture_recognizer.task	# 默认的模型文件
│   └── self_defined
├── README.md
├── result_handler.py	# 返回的结果分析模块
└── test.py				# 测试运行

```

