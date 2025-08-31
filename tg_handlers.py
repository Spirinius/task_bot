from taskdb import Tasks, db_init

from beanie import PydanticObjectId

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards as kb

router = Router()

class Task(StatesGroup):
    task = State()

class editTask(StatesGroup):
    editing = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello there! this is a task bot, here can you add your tasks, read, point as complite and delete them', reply_markup=kb.add_key_board)

@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("There are commands for using TaskBot:\n/add : adding a new task\n/list : a list off exist tasks")

@router.message(Command('add'))
async def add_command(message: Message, state: FSMContext):
    await message.answer("Write your task")
    await state.set_state(Task.task)

@router.message(Task.task)
async def add_task(message: Message, state: FSMContext):
    task = message.text
    new_task = Tasks(user_id = message.from_user.id, task = task)
    await new_task.insert()
    await message.answer("Task added")
    await state.clear()

@router.message(Command('list'))
async def list_command(message: Message):
    list_of_tasks = await Tasks.find(Tasks.user_id == message.from_user.id).to_list()

    if not list_of_tasks:
        await message.answer("У тебя пока нет задач 👌")
        return

    # Собираем список строк
    for i, task in enumerate(list_of_tasks): 
        tasks_text = (f"{i+1}. {task.task} {'✅' if task.done else '❌'}")
        await message.answer(tasks_text,reply_markup=kb.change_state_of_task(task.id ,task.done))
    
@router.callback_query(F.data.startswith('done:'))
async def done(callback: CallbackQuery):
    _, idx = callback.data.split(":")
    task = await Tasks.find_one(Tasks.id == PydanticObjectId(idx))
    task.done = not task.done
    await task.save()
    await callback.answer('')
    
    user_id = callback.from_user.id
    list_of_tasks = await Tasks.find(Tasks.user_id == callback.from_user.id).to_list()

    # Собираем список строк
    tasks_text = "ds"
    for i, taskIn in enumerate(list_of_tasks): 
        if taskIn == task:
            tasks_text = (f"{i+1}. {taskIn.task} {'✅' if taskIn.done else '❌'}")
            break
    await callback.message.edit_text(tasks_text,reply_markup=kb.change_state_of_task(task.id ,task.done))

@router.callback_query(F.data.startswith('edit:'))
async def edit(callback: CallbackQuery, state: FSMContext):
    _, idx = callback.data.split(":")
    task = await Tasks.find_one(Tasks.id == PydanticObjectId(idx))
    await state.update_data(task_id = idx)
    await callback.message.answer('Write your task')
    await state.set_state(editTask.editing)

@router.message(editTask.editing)
async def edit_task(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get("task_id")

    task = await Tasks.get(PydanticObjectId(task_id))  # <-- вот оно

    task.task = message.text
    await task.save()  # сохраняем изменения

    await state.clear()

    list_of_tasks = await Tasks.find(Tasks.user_id == message.from_user.id).to_list()

    if not list_of_tasks:
        await message.answer("У тебя пока нет задач 👌")
        return

    # Собираем список строк
    for i, task in enumerate(list_of_tasks): 
        tasks_text = (f"{i+1}. {task.task} {'✅' if task.done else '❌'}")
        await message.answer(tasks_text,reply_markup=kb.change_state_of_task(task.id ,task.done))

@router.callback_query(F.data.startswith('delete:'))
async def delete(callback: CallbackQuery):
    _, idx = callback.data.split(":")
    task = await Tasks.find_one(Tasks.id == PydanticObjectId(idx))
    await task.delete()
    await callback.message.delete()

