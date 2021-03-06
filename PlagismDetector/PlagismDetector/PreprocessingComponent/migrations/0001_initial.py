# Generated by Django 3.1.4 on 2021-03-17 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataDocumentName', models.CharField(max_length=200)),
                ('DataDocumentType', models.CharField(max_length=10)),
                ('DataDocumentAuthor', models.CharField(max_length=100)),
                ('DataDocumentFile', models.FileField(upload_to='DocumentFile/')),
            ],
        ),
        migrations.CreateModel(
            name='DataDocumentContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataDocumentSentence', models.CharField(max_length=200)),
                ('DataDocumentSentenceLength', models.IntegerField(default=0)),
                ('DataDocumentNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PreprocessingComponent.datadocument')),
            ],
        ),
        migrations.AddIndex(
            model_name='datadocumentcontent',
            index=models.Index(fields=['DataDocumentNo', 'DataDocumentSentence'], name='DataDocumentNo_idx'),
        ),
        migrations.AddIndex(
            model_name='datadocumentcontent',
            index=models.Index(fields=['DataDocumentSentence'], name='DataDocumentSentence_idx'),
        ),
    ]
