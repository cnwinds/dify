import React, { Fragment } from 'react'
import { ProviderEnum } from '../declarations'
import type { ProviderConfig } from '../declarations'

const SmallText = () => <span className='text-sm'>BAAI</span>
const Icon = React.memo(SmallText)
const NormalText = () => <span >BAAI</span>
const Text = React.memo(NormalText)

const config: ProviderConfig = {
  selector: {
    name: {
      'en': 'BAAI',
      'zh-Hans': 'BAAI',
    },
    icon: <Icon />,
  },
  item: {
    key: ProviderEnum.baai,
    titleIcon: {
      'en': <Text />,
      'zh-Hans': <Text />,
    },
  },
  modal: {
    key: ProviderEnum.baai,
    title: {
      'en': 'BAAI',
      'zh-Hans': 'BAAI',
    },
    icon: <Fragment />,
    link: {
      href: '',
      label: {
        'en': 'BAAI website',
        'zh-Hans': '访问BAAI',
      },
    },
    validateKeys: [],
    fields: [],
    defaultValue: {},
  },
}

export default config
