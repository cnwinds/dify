import { Fragment } from "react";
import { ProviderEnum } from "../declarations";
import type { ProviderConfig } from "../declarations";
import React from "react";

const Icon = React.memo(() => <span className='text-sm'>MokaAI</span>)
const Text = React.memo(() => <span>Moka AI</span>)

const config: ProviderConfig = {
  selector: {
    name: {
      en: "Moka AI",
      "zh-Hans": "Moka AI",
    },
    icon: <Icon />,
  },
  item: {
    key: ProviderEnum.mokaai,
    titleIcon: {
      en: <Text />,
      "zh-Hans": <Text />,
    },
  },
  modal: {
    key: ProviderEnum.mokaai,
    title: {
      en: "Moka AI",
      "zh-Hans": "Moka AI",
    },
    icon: <Fragment />,
    link: {
      href: "https://huggingface.co/moka-ai",
      label: {
        en: "Moka AI website",
        "zh-Hans": "访问Moka AI",
      },
    },
    validateKeys: [],
    fields: [],
    defaultValue: {}
  },
};

export default config;
