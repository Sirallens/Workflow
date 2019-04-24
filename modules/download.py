import models.tables as mdls
def prepare_download(db, folio):
    request_for_download = mdls.request.query.filter_by(folio=folio).first()
    download_pack = dict()
    download_pack['filename'] = request_for_download.filename
    download_pack['data'] = request_for_download.file
    return download_pack