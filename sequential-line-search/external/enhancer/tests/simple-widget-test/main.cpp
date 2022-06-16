#include <enhancer/enhancerwidget.hpp>
#include <QApplication>

int main(int argc, char** argv)
{
    QApplication app(argc, argv);

    Q_INIT_RESOURCE(enhancer_resources);

#if defined(__APPLE__)
    QSurfaceFormat format;
    format.setVersion(3, 2);
    format.setProfile(QSurfaceFormat::CoreProfile);
    QSurfaceFormat::setDefaultFormat(format);
#endif

    enhancer::EnhancerWidget widget;
    widget.setImage(QImage("://test-images/DSC03039.JPG"));
    widget.setParameters({ 0.6, 0.4, 0.6, 0.6, 0.5, 0.5 });
    widget.show();
    return app.exec();
}
