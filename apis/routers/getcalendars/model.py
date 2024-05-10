from sqlalchemy import select, func
from fastapi import status, HTTPException
from pydantic import BaseModel
import datetime
import calendar
from .schema import Response, TokenData, Data
from apis.services.authfunctions import database
from apis.bases.exercise_done import ExerciseDone

class Model(BaseModel):
    async def exec(self, year: int, month: int, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        
        # exercise_doneから、対象期間内の該当するuser_idかつdone=trueであるdateを、重複行を除外してselectする
        query = select(ExerciseDone.date).where(
            ExerciseDone.user_id == token.uid,
            ExerciseDone.done == True,
            func.year(ExerciseDone.date) == year,
            func.month(ExerciseDone.date) == month
            ).group_by(ExerciseDone.date)
        res = await database.fetch_all(query)

        # resから、dateのみのリストを作る。
        date_list = [item['date'] for item in res]

        # 対象月の最初の日と最後の日を取得
        first_day = datetime.date(year, month, 1)
        last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])

        # dataリストを初期化
        arry = []

        # 1日ずつループ
        current_day = first_day
        while current_day <= last_day:
            # current_dayがdate_listに含まれていたら、done = true
            if current_day in date_list:
                done = True 
            # 含まれていなかったら、done = false
            else:
                done = False

            # Dataを作ってarryに追加。
            dt = Data(
                day = current_day,
                exerciseDone = done
            )
            arry.append(dt)
            current_day += datetime.timedelta(days=1)
        
        # Responseを返す。
        return Response(status=1, data=arry)
