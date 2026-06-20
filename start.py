await state.set_state(Onboarding.yonalish)
@router.message(Onboarding.ota_raqam, F.text)
async def get_raqam_text(message: Message, state: FSMContext):
    raqam = message.text.strip()
    if not re.match(r'^\+998\d{9}$', raqam):
        await message.answer("❌ Raqam noto'g'ri!\nTo'g'ri format: +998901234567\nQaytadan kiriting:")
        return
    await state.update_data(ota_raqam=raqam)
    await _keyin_raqam(message, state)

@router.callback_query(F.data == "kasb_orqaga", Onboarding.kasb_tasdiqlash)
async def kasb_orqaga_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.delete()
    await call.message.answer(
        f"Boshqa kasb tanlang 👇",
        reply_markup=kasb_keyboard(data["yonalish"])
    )
    await state.set_state(Onboarding.kasb_tanlash)

@router.callback_query(F.data == "yonalish_orqaga", Onboarding.kasb_tasdiqlash)
async def yonalish_orqaga_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer()
