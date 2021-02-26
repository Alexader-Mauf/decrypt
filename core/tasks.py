from . import models


def run_open_transfers():
    transactions = models.BankTransfer.objects.filter(is_open=True).all()
    success_ids = []
    faiL_ids = []
    for trans in transactions:
        trans.run_transfer()
        if trans.is_success:
            success_ids.append(trans.id)
        else:
            faiL_ids.append(trans.id)

    return {"success_ids": success_ids, "faiL_ids": faiL_ids}