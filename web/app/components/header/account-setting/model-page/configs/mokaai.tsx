import React, { Fragment } from 'react'
import { ProviderEnum } from '../declarations'
import type { ProviderConfig } from '../declarations'

const SmallText = () => <span className='text-sm'>MokaAI</span>
const Icon = React.memo(SmallText)
const NormalText = () => <span >Moka AI</span>
const Text = React.memo(NormalText)

const config: ProviderConfig = {
  selector: {
    name: {
      'en': 'Moka AI',
      'zh-Hans': 'Moka AI',
    },
    icon: <Icon />,
  },
  item: {
    key: ProviderEnum.mokaai,
    titleIcon: {
      'en': <Text />,
      'zh-Hans': <Text />,
    },
  },
  modal: {
    key: ProviderEnum.mokaai,
    title: {
      'en': 'Moka AI',
      'zh-Hans': 'Moka AI',
    },
    icon: <Fragment />,
    link: {
      href: 'https://huggingface.co/moka-ai',
      label: {
        'en': 'Moka AI website',
        'zh-Hans': '访问Moka AI',
      },
    },
    validateKeys: [],
    fields: [],
    defaultValue: {},
  },
}

export default config
