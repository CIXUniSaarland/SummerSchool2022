cmake_minimum_required(VERSION 3.1)

project(enhancer CXX)
set(CMAKE_CXX_STANDARD 11)

option(ENHANCER_USE_QT_FEATURES "Build Qt features" OFF)
option(ENHANCER_BUILD_QT_TESTS "Build Qt-based tests" OFF)

set(ENHANCER_VERT_SHADER_PATH "${CMAKE_CURRENT_SOURCE_DIR}/shaders/enhancer.vs" CACHE INTERNAL "")
set(ENHANCER_FRAG_SHADER_PATH "${CMAKE_CURRENT_SOURCE_DIR}/shaders/enhancer.fs" CACHE INTERNAL "")

file(GLOB headers ${CMAKE_CURRENT_SOURCE_DIR}/include/enhancer/*.hpp)
file(GLOB sources ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

if(ENHANCER_USE_QT_FEATURES)
  find_package(Eigen3 REQUIRED)
  find_package(Qt5Gui REQUIRED)
  find_package(Qt5Widgets REQUIRED)

  set(CMAKE_AUTORCC ON)
  qt5_add_resources(resources ${CMAKE_CURRENT_SOURCE_DIR}/enhancer-resources.qrc)

  add_library(enhancer STATIC ${headers} ${sources} ${resources})
  target_link_libraries(enhancer Eigen3::Eigen Qt5::Gui Qt5::Widgets)
  target_include_directories(enhancer PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>	$<INSTALL_INTERFACE:include>)
  install(FILES ${headers} DESTINATION include/enhancer)
  install(TARGETS enhancer ARCHIVE DESTINATION lib)

  if(ENHANCER_BUILD_QT_TESTS)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests/simple-widget-test)
  endif()
else()
  add_library(enhancer INTERFACE)
  target_sources(enhancer INTERFACE ${headers})
  target_include_directories(enhancer INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)
  install(FILES ${headers} DESTINATION include)
endif()
