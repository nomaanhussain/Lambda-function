import whisper
import json
import os
import boto3
import urllib.parse

model = whisper.load_model("local_base.pt")
    
def format_timestamp(seconds: float, always_include_hours: bool = False, decimal_marker: str = '.'):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    try:
        print("Received event: " + json.dumps(event, indent=2))

        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        
        # save s3 mp3 file to tmp folder
        local_file_name = '/tmp/'+ key.split('/')[-1]
        print(local_file_name)
        print(bucket, key)
        s3.Bucket(bucket).download_file(key, local_file_name)
        lst = os.listdir("/tmp")
        print(lst)
    
        # run whisper transcribe model on mp3 file
        result = model.transcribe(local_file_name)

        transcription = result["text"]
        encoded_string = transcription.encode("utf-8")

        audio_basename = key.split('/')[-1].replace(".mp3", "")
        file_name = audio_basename + '.txt' 
        s3_path = "transcriptions/" + file_name

        # save the transcription to S3 bucket
        s3.Bucket(bucket).put_object(Key=s3_path, Body=encoded_string)


        # save SRT
        srt_file_path = '/tmp/' + audio_basename + '.srt'
        with open(srt_file_path, "w", encoding="utf-8") as srt:
            for i, segment in enumerate(result["segments"], start=1):
                # write srt lines
                print(
                    f"{i}\n"
                    f"{format_timestamp(segment['start'], always_include_hours=True, decimal_marker=',')} --> "
                    f"{format_timestamp(segment['end'], always_include_hours=True, decimal_marker=',')}\n"
                    f"{segment['text'].strip().replace('-->', '->')}\n",
                    file=srt,
                    flush=True,
                )

        lst = os.listdir("/tmp")
        print(lst)

        # upload srt file to S3 bucket
        file_name = audio_basename + '.srt'
        s3_path = "srt/" + file_name
        s3 = boto3.client('s3')
        s3.upload_file(srt_file_path, bucket, s3_path)
        
    except Exception as e:
        print(str(e))
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }


if __name__ == "__main__":

    lambda_handler(None, None)