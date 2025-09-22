import "https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@3.0.1/dist/cookieconsent.umd.js";

CookieConsent.run({
      disablePageInteraction: false,

      guiOptions: {
        consentModal: {
          layout: "box",
          position: "bottom left",
        },
      },

      categories: {
        necessary: {
          enabled: true, // this category is enabled by default
          readOnly: true, // this category cannot be disabled
        },
        analytics: {},
        ads: {},
      },

      language: {
        default: "en",
        translations: {
          en: async () => {
            const res = await fetch(
              "/website_cookieconsent/static/src/i18n/en.json"
            );
            return await res.json();
          },
          fr: async () => {
            const res = await fetch(
              "/website_cookieconsent/static/src/i18n/fr.json"
            );
            return await res.json();
          },
        },
      },

});
