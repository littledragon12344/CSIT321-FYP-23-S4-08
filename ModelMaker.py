from mediapipe_model_maker import gesture_recognizer


# https://www.youtube.com/watch?v=yOP_FY2KTm8
#Train a model (1)

# Load the dataset
data = gesture_recognizer.Dataset.from_folder(dirname='images')
train_data, validation_data = data.split(0.8)

#Train the custom model
model = gesture_recognizer.GestureRecognizer.create(
	train_data=train_data,
	validation_data=validation_data,
	hparams=gesture_recognizer.HParasms(export_dir=export_dir)
)

#Train a model (2)
#evaluate using unseen data
metric = model.evaluate(test_data)

#export as model
model.export_model(model_name='bruh.task')