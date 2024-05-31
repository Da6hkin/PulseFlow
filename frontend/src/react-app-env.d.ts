/* eslint-disable */

/// <reference types="node" />
/// <reference types="react" />
/// <reference types="react-dom" />

declare namespace NodeJS {
  interface ProcessEnv {
    readonly NODE_ENV: 'development' | 'production'
    readonly PUBLIC_URL: string
  }
}

declare module '*.png' {
  const src: string
  export default src
}

declare module '*.svg' {
  import type * as React from 'react'

  export const ReactComponent: React.FunctionComponent<React.SVGProps<
  SVGSVGElement
  > & { title?: string }>

  const src: string
  export default src
}

