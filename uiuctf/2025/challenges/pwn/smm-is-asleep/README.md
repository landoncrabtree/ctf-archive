# SMM Is Asleep

## Description

The engineers at SIGPwny Inc. is up to some shenanigans again in SMM.
They totally thought it was safe to expose the write API of SmmLockBox
to the OS. Unfortunately the secrets (flag) at physical address 0x44440000
got leaked again, and it's only readable from SMM! How was this possible?

`$ socat file:$(tty),raw,echo=0 openssl:smm-is-asleep.chal.uiuc.tf:1337`

  <details><summary>Show hint</summary>According to the logs, the attacker put the system to S3 sleep for a
  brief period of time.</details>

**author**: YiFei Zhu

## Files

* [README](files/README)

* [chal_build.tar.zst](files/chal_build.tar.zst)

* [edk2debug.log](files/edk2debug.log)

* [edk2_artifacts.tar.zst](files/edk2_artifacts.tar.zst)

* [run.tar.zst](files/run.tar.zst)

