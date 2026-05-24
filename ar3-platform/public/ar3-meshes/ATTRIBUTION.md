# AR3 mesh assets

The seven `.STL` files in this directory and the `public/ar3.urdf`
robot description are derived from:

> **ar3_core** by Dexter Ong
> https://github.com/ongdexter/ar3_core
> Licensed under the MIT License — Copyright (c) 2021 Dexter Ong

## Local adaptations

- Mesh paths in the URDF were rewritten from
  `package://ar3_description/meshes/...` to `/ar3-meshes/...` so the
  app can serve them from the Vite `public/` directory.
- All six joints were changed from `type="continuous"` to
  `type="revolute"` and given explicit `<limit lower upper>` elements
  that match the AR3 firmware. No other URDF content was modified.

## Fallback model

`public/ar3-cylinders.urdf` is the original hand-built cylinder-based
URDF used through M0–M4. Swap it back in by changing the path in
`src/scene/Viewer.tsx` if the real meshes need debugging.

## MIT License (excerpt)

```
Copyright (c) 2021 Dexter Ong

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
```
