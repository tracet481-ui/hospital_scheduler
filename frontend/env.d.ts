/// <reference types="vite/client" />

/// vue dosyası tanınmaması durumunda 

/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}


