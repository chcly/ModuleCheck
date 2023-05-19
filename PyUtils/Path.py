import os, sys
import subprocess
import shutil

class Path:

    def __init__(self, directory=None):

        if (directory != None):
            self._path = directory
            self.normalize()
        else:
            self._path = os.getcwd()
            self.normalize()

        if (not self.check()):
            msg = "The supplied path %s is invalid" % self._path
            raise IOError(msg)

    def normalize(self):

        if (sys.platform == "win32"):
            self._path = self._path.replace('/', '\\')
        else:
            self._path = self._path.replace('\\', '/')
 
        self._path = os.path.abspath(self._path)

    def check(self):
        return os.path.exists(self._path)

    def __repr__(self) -> str:
        return self._path

    def back(self, n=1):
        back = self._path
        for _ in range(n):
            back = os.path.join(back, "../")
        return Path(back)

    def join(self, oth):
        result = self._path
        return Path(os.path.join(result, oth))

    def file(self, path):
        return self.join(path)

    def open(self, name, mode="r"):
        result = os.path.join(self._path, name)
        if (os.path.isfile(result)):
            return open(result, mode)
        raise FileNotFoundError

    def create(self, relative):
        result = self._path

        if (sys.platform == "win32"):
            relative = relative.replace('/', '\\')
        else:
            relative = relative.replace('\\', '/')

        joinResult = os.path.join(result, relative)
        if (not os.path.isdir(joinResult)):
            os.makedirs(joinResult)

        return Path(joinResult)

    def subdir(self, relative):

        result = self._path
        if (sys.platform == "win32"):
            relative = relative.replace('/', '\\')
        else:
            relative = relative.replace('\\', '/')

        joinResult = os.path.join(result, relative)
        if (not os.path.isdir(joinResult)):
            msg = "The path '%s' does not exist " % joinResult
            raise FileNotFoundError(msg)

        return Path(joinResult)

    def recreate(self):
        result = self._path

        os.makedirs(result)
        return Path(result)

    def remove(self):
        def onerror(func, path, exc_info):
            """
            Error handler for ``shutil.rmtree``.

            If the error is due to an access error (read only file)
            it attempts to add write permission and then retries.

            If the error is for another reason it re-raises the error.
            
            Usage : ``shutil.rmtree(path, onerror=onerror)``
            """
            import stat
            # Is the error an access error?
            if not os.access(path, os.W_OK):
                os.chmod(path, stat.S_IWUSR)
                func(path)
            else:
                raise IOError

        if (os.path.isdir(self._path)):
            shutil.rmtree(self._path, onerror=onerror, ignore_errors=False)

    def copyTo(self, file, toPath):
        shutil.copyfile(self.file(file), toPath.file(file))
        shutil.copymode(self.file(file), toPath.file(file))

    def copyTree(self, toPath):
        shutil.copytree(self._path, toPath.path, dirs_exist_ok=True)

    def removeFile(self, file):
        localFile = os.path.join(self._path, file)
        if (os.path.isfile(localFile)):
            os.remove(localFile)

    def goto(self):
        try:
            os.chdir(self._path)
        except IOError:
            msg = "Failed to change working directory to %s" % str(self)
            raise IOError(msg)
        return self

    def run(self, cmd):
        subprocess.run(cmd, shell=True, env=os.environ)