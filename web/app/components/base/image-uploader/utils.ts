import { upload } from '@/service/base'

type ImageUploadParams = {
  file: File
  onProgressCallback: (progress: number) => void
  onSuccessCallback: (res: { id: string }) => void
  onErrorCallback: () => void
}
type ImageUpload = (v: ImageUploadParams, isPublic?: boolean) => void
export const imageUpload: ImageUpload = ({
  file,
  onProgressCallback,
  onSuccessCallback,
  onErrorCallback,
}, isPublic) => {
  const formData = new FormData()
  formData.append('file', file)
  const onProgress = (e: ProgressEvent) => {
    if (e.lengthComputable) {
      const percent = Math.floor(e.loaded / e.total * 100)
      onProgressCallback(percent)
    }
  }

  upload({
    xhr: new XMLHttpRequest(),
    data: formData,
    onprogress: onProgress,
  }, isPublic)
    .then((res: { id: string }) => {
      onSuccessCallback(res)
    })
    .catch(() => {
      onErrorCallback()
    })
}
