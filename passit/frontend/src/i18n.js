import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import pl from "./consts/translations/pl";
import en from "./consts/translations/en";

i18n
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    resources: { pl, en },
    lng: "pl",
    keySeparator: false, // we do not use keys in form messages.welcome
    interpolation: {
      escapeValue: false // react already safes from xss
    },
    react: {
      wait: true,
      useSuspense: false,
    },
  });


export default i18n;
