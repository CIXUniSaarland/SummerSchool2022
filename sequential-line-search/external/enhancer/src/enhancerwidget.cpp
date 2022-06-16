#include <enhancer/enhancerwidget.hpp>
#include <QOpenGLShaderProgram>
#include <QOpenGLTexture>
#include <iostream>

#define TEXTURE_UNIT_ID 0

namespace enhancer
{
    EnhancerWidget::EnhancerWidget(QWidget* parent) :
    QOpenGLWidget(parent),
    dirty_(true)
    {
        image_ = QImage(64, 64, QImage::Format_RGBA8888);
        image_.fill(Qt::GlobalColor::darkGray);

        parameters_.fill(0.5);
    }

    EnhancerWidget::~EnhancerWidget()
    {
        makeCurrent();
        vbo.destroy();
        vao.destroy();
        texture_->destroy();
        doneCurrent();
    }

    void EnhancerWidget::setImage(const QImage& image)
    {
        image_ = image;
        dirty_ = true;
    }

    void EnhancerWidget::initializeGL()
    {
        const bool is_opengl_ready = initializeOpenGLFunctions();

        if (!is_opengl_ready)
        {
            std::cerr << "Error: Failed to prepare OpenGL profile." << std::endl;
            exit(1);
        }

        const GLubyte* opengl_version = glGetString(GL_VERSION);
        const GLubyte* glsl_version = glGetString(GL_SHADING_LANGUAGE_VERSION);
        std::cout << "OpenGL Version: " << opengl_version << std::endl;
        std::cout << "GLSL Version: " << glsl_version << std::endl;

        vao.create();
        vbo.create();

        vao.bind();
        vbo.bind();
        {
            constexpr GLfloat vertex_data[] =
            {
                -1.0, -1.0,
                +1.0, -1.0,
                +1.0, +1.0,
                -1.0, +1.0,
            };
            vbo.allocate(vertex_data, sizeof(vertex_data) * sizeof(GLfloat));
        }
        vbo.release();
        vao.release();

        QOpenGLShader *vertex_shader = new QOpenGLShader(QOpenGLShader::Vertex, this);
        vertex_shader->compileSourceFile("://shaders/enhancer.vs");

        QOpenGLShader *fragment_shader = new QOpenGLShader(QOpenGLShader::Fragment, this);
        fragment_shader->compileSourceFile("://shaders/enhancer.fs");

        program_ = std::make_shared<QOpenGLShaderProgram>();
        program_->addShader(vertex_shader);
        program_->addShader(fragment_shader);
        program_->link();

        program_->bind();
        {
            program_->setUniformValue("texture_sampler", TEXTURE_UNIT_ID);
        }
        program_->release();
    }

    void EnhancerWidget::paintGL()
    {
        glClearColor(0.0, 0.0, 0.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        const int image_width = this->image_.width();
        const int image_height = this->image_.height();
        const int w = width() * devicePixelRatio();
        const int h = height() * devicePixelRatio();
        if (w * image_height == h * image_width)
        {
            glViewport(0, 0, w, h);
        }
        else if (w * image_height > h * image_width)
        {
            const int w_corrected = h * image_width / image_height;
            glViewport((w - w_corrected) / 2, 0, w_corrected, h);
        }
        else if (w * image_height < h * image_width)
        {
            const int h_corrected = w * image_height / image_width;
            glViewport(0, (h - h_corrected) / 2, w, h_corrected);
        }

        if (dirty_)
        {
            texture_ = std::make_shared<QOpenGLTexture>(image_.mirrored(), QOpenGLTexture::DontGenerateMipMaps);
            dirty_ = false;
        }

        program_->bind();
        vao.bind();
        vbo.bind();
        texture_->bind(TEXTURE_UNIT_ID);
        {
            program_->enableAttributeArray("vertex_position");
            program_->setAttributeBuffer("vertex_position", GL_FLOAT, 0, 2, 2 * sizeof(GLfloat));

            program_->setUniformValueArray("parameters", parameters_.data(), 6, 1);

            glDrawArrays(GL_TRIANGLE_FAN, 0, 4);
            program_->disableAttributeArray("vertex_position");
        }
        texture_->release();
        vbo.release();
        vao.release();
        program_->release();
    }

    void EnhancerWidget::resizeGL(int width, int height)
    {
    }
}
