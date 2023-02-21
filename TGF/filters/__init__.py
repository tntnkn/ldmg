from aiogram    import Dispatcher

from .user import isPromtingForUserInfo, isFillingUserInfoForm, isSelectingUserConditionsOptions


def setup(dp: Dispatcher):
    dp.filters_factory.bind(isPromtingForUserInfo)
    dp.filters_factory.bind(isFillingUserInfoForm)
    dp.filters_factory.bind(isSelectingUserConditionsOptions)

