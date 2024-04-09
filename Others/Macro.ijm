dir = "your_path";
list = getFileList(dir);

for (i = 0; i < list.length; i++) {
    file = list[i];
    if (endsWith(file, ".tif")) {
        open(dir + file);
        selectWindow(file);
        run("Subtract Background...", "rolling=100 light");
        saveAs("Tiff", dir + "processed_" + file);
        close();
    }
}

