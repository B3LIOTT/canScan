
from modules import *
from time import sleep


def dispose(printer, writer, file, notifier, bus):
    printer.stop()
    writer.stop()
    file.close()
    notifier.stop()
    bus.shutdown()


config, file_path = load_config()
zoomies = listen(config=config, file_path=file_path)

try:
    wake_up_maestro()
except Exception as e:
    os.remove(file_path)
    dispose(*zoomies)
    print("The file has been deleted due to an error: ", e)
    exit(1)

dispose(*zoomies)
end_checks(file_path)
