from wtforms import StringField, SubmitField, FileField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

subject_choices = [('','Select Subject'),('Math','Math'),('Science','Science')]
standard_choices = [('','Select Standard'),('9','9')]


class VideoUploadForm(FlaskForm):
	subject = SelectField('Select Subject', validators=[DataRequired()], choices = subject_choices )
	standard = SelectField('Select Standard', validators=[DataRequired()], choices = standard_choices )
	chapter = StringField('Chepter title', validators=[DataRequired(), Length(min=4, max =50)])
	videoUrl = StringField('Video Url', validators=[Length(min=3, max =50)])
	file = FileField('Select File', validators=[FileAllowed(['mp4', 'avi'], 'mp4 or avi only!')])
	submit = SubmitField('Upload Video')