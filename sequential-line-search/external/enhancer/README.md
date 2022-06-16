# enhancer

A C++11 / GLSL library for enhancing photographs (adjusting brightness, contrast, etc.).

This repository contains the following three features:
- __GLSL shaders__: Enhancement functionality as shaders for real-time enhancement applications.
- __C++ functions__: Enhancement functionality as C++ functions for display-less environments.
- __Qt Widget__: Utility Qt-based widget for easing the use of the GLSL shaders.

## Supported Parameters

- Brightness
- Contrast
- Saturation
- Color Balance
  - Red
  - Green
  - Blue

## Required Runtime Environments

- GLSL 3.3
- OpenGL 3.2 Core Profile (for Qt features only)

## Dependencies

### C++ Features

- Eigen

### C++ Qt Features

- Qt5

## C++ API

```
Eigen::Vector3d enhance(const Eigen::Vector3d& input_rgb,
                        const Eigen::VectorXd& parameters);
```
where `input_rgb` is a 3-dimensional vector (\[0, 1\]^3), and `parameters` is a 6-dimensional vector (\[0, 1\]^6).

## Projects using enhancer

- Sequential Line Search <https://github.com/yuki-koyama/sequential-line-search>
- SelPh <https://github.com/yuki-koyama/selph>
