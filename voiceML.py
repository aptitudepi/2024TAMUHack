import nemo.collections.asr as nemo_asr
speaker = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained("nvidia/speakerverification_en_titanet_large")

embedding = speaker.get_embedding("captured1.wav")
speaker.verify_speakers("captured1.wav", "captured2.wav")
