from sqlalchemy import select
from fastapi import status, HTTPException
from pydantic import BaseModel
from datetime import date
from .schema import Response, TokenData, Data
from apis.services.authfunctions import database
from apis.bases.exercise import Exercise
from apis.bases.exercise_selected import ExerciseSelected
from apis.bases.exercise_done import ExerciseDone

class Model(BaseModel):
    async def exec(self, date: date, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        
        # exerciseから全ての項目をid昇順にセレクトする。→res_exe
        query = select(Exercise).order_by(Exercise.id)
        res_exe = await database.fetch_all(query)

        # exercise_doneから該当するuser_id,dateのexercise_idを全てselectする→res_done
        query = select(ExerciseDone.exercise_id).where(ExerciseDone.user_id == token.uid, ExerciseDone.date == date)
        res_done = await database.fetch_all(query)

        # exercise_selectedから該当するuser_idのexercise_idを全てselectする→res_selected
        query = select(ExerciseSelected.exercise_id).where(ExerciseSelected.user_id == token.uid,)
        res_selected = await database.fetch_all(query)

        # res_done,res_selectedそれぞれから、exercise_idのみのリストを作る。
        done_list = [item['exercise_id'] for item in res_done]
        selected_list = [item['exercise_id'] for item in res_selected]
        
        # dataリストを初期化
        arry = []
        for exe in res_exe:
            # idがdone_listに含まれていたら、done = true
            if exe.id in done_list:
               done = True 
            # idがselected_listのみに含まれていたら、done = False
            elif exe.id in selected_list:
               done = False 
            # idがどちらにも含まれていなかったら、Dataに加えない。
            else:
                continue

            # Dataを作ってarryに追加。
            dt = Data(
                exerciseId = exe.id,
                exerciseName = exe.exercise_name,
                exerciseDone = done,
            )
            arry.append(dt)

        # Responseを返す。
        return Response(status=1, data=arry)
