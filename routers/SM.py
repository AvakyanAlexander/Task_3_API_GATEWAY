# СМ (Система управления) – для привязки документов к карточкам контрактов.
from sqlalchemy.future import select
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models import Document, Contract, Сontract_Documentt
from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from auth.jwt_token import decode_token

router = APIRouter(
    prefix="/api/v1/SM",
    tags=["SM"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


@router.post("/create_contract")
async def create_contract(name: str,
                          desc: str,
                          token: str = Depends(oauth2_scheme),
                          db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401,
                            detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None:
        raise HTTPException(status_code=401,
                            detail="Пользователь не найден в токене")
    new_contract = Contract(con_name=name, description=desc)
    db.add(new_contract)
    await db.commit()
    await db.refresh(new_contract)
    return new_contract


@router.get("/get_contract/{con_id}")
async def read_contract(con_id: int,
                        token: str = Depends(oauth2_scheme),
                        db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401,
                            detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None:
        raise HTTPException(status_code=401,
                            detail="Пользователь не найден в токене")
    result = await db.execute(select(Contract).filter(Contract.con_id == con_id))
    contract = result.scalars().first()
    if contract is None:
        raise HTTPException(status_code=404,
                            detail="Запрошенный контракт не найден")

    return {
        "con_id": contract.con_id,
        "con_name": contract.con_name,
        "description": contract.description,
        "create_date": contract.create_date
    }


@router.get("/get_all_contract")
async def read_all_contract(token: str = Depends(oauth2_scheme),
                            db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401,
                            detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None:
        raise HTTPException(status_code=401,
                            detail="Пользователь не найден в токене")
    query = await db.execute(select(Contract))
    contracts = query.scalars().all()
    if contracts is None:
        raise HTTPException(status_code=404, detail="Контракты не найдены")
    return {"contract_list": contracts}


@router.delete("/delete_contract/{contract_id}")
async def delete_contract(contract_id: int,
                          token: str = Depends(oauth2_scheme),
                          db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401,
                            detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None:
        raise HTTPException(status_code=401,
                            detail="Пользователь не найден в токене")
    result = await db.execute(select(Contract).filter(Contract.con_id == contract_id))
    contract = result.scalars().first()

    if contract is None:
        raise HTTPException(status_code=404,
                            detail="Контракт на удаление не найден")


    await db.delete(contract)
    await db.commit()

    return {"detail": "Контракт успешно удален"}


@router.post("/connect_contract_document")
async def connect_doc_contract(contract_idd: int,
                               document_idd: int,
                               token: str = Depends(oauth2_scheme),
                               db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401,
                            detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None:
        raise HTTPException(status_code=401,
                            detail="Пользователь не найден в токене")
    new_connect = Сontract_Documentt(contract_id=contract_idd, document_id=document_idd)
    db.add(new_connect)
    await db.commit()
    await db.refresh(new_connect)
    return {"msg": "Документ успешно привязан к контракту",
            "id_con_doc": new_connect.con_doc_id,
            "date": new_connect.date_bind
            }


@router.get("/read_contract_document/{con_doc_id}")
async def read_doc_contract(con_doc_id: int,
                            token: str = Depends(oauth2_scheme),
                            db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401,
                            detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None:
        raise HTTPException(status_code=401,
                            detail="Пользователь не найден в токене")
    result = await db.execute(select(Сontract_Documentt).filter(Сontract_Documentt.con_doc_id == con_doc_id))
    contract_document = result.scalars().first()
    result = await db.execute(select(Document).filter(Document.doc_id == contract_document.document_id))
    document = result.scalars().first()
    result = await db.execute(select(Contract).filter(Contract.con_id == contract_document.contract_id))
    contract = result.scalars().first()
    if contract_document is None:
        raise HTTPException(status_code=404,
                            detail="Привязанный документ к контракту не найден")

    return {
        "Документ": f"Привязан к контракту(id {contract_document.contract_id})",
        "file_name": document.file_name,
        "file_type": document.file_type,
        "Контракт": f"Привязан к документу(id {contract_document.document_id})",
        "con_name": contract.con_name,
        "description": contract.description,
        "Дата привязки": contract_document.date_bind
    }
