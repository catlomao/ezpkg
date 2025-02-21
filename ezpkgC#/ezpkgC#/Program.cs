using System;
using System.IO;
using Newtonsoft.Json;
using Spectre.Console;
namespace ezpkg
{
    internal class Program
    {
        static string removeNewLine(string output)
        {
            string returnvalue = output.Replace("\n", "").Replace("\r", "");
            return returnvalue;
        }
        static int hiddenrun(string cmd)
        {
            try
            {
                var startInfo = new System.Diagnostics.ProcessStartInfo
                {
                    WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden,
                    FileName = "powershell.exe",
                    Arguments = $"-Command \"{cmd}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = new System.Diagnostics.Process { StartInfo = startInfo })
                {
                    process.Start();
                    string output = process.StandardOutput.ReadToEnd().Trim();
                    process.WaitForExit();
                    return process.ExitCode == 0 && output.Equals("True", StringComparison.OrdinalIgnoreCase) ? 0 : 1;
                }
            }
            catch
            {
                return 1; // An exception occurred
            }
        }

        static void Main()
        {
            Console.WriteLine("Welcome to ezpkg cli do h (or help) for commands");
            var ogpath = Environment.GetEnvironmentVariable("SystemDrive");
            var SYSpath = removeNewLine(ogpath);
            var ezpkgpath = SYSpath + "\\ezpkg";
            // Check if the directory exists
            if (!Directory.Exists(ezpkgpath))
            {
                Console.WriteLine("\u001b[1;33mHmm.. it seems like C:\\ezpkg\\ is not found, lemme create it for you....\u001b[0m");

                try
                {
                    // Create the main directory and subdirectories
                    Directory.CreateDirectory(ezpkgpath);
                    Directory.CreateDirectory(Path.Combine(ezpkgpath, "temp"));
                    Directory.CreateDirectory(Path.Combine(ezpkgpath, "packages"));

                    Console.WriteLine("\u001b[1;32mDONE, ENJOY!\u001b[0m");
                }
                catch (UnauthorizedAccessException)
                {
                    Console.WriteLine("\u001b[41mError: You do not have permission to create the directory.\x1b[0m");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"\u001b[41mAn unexpected error occurred: {ex.Message}\x1b[0m");
                }
            }
            else
            {
                Console.WriteLine("\u001b[1;31mezpkg setup already exists! Ignoring....\u001b[0m");
            }
            while (true)
            {

                var color1 = "\x1b[1;32m"; // ANSI escape for green
                var color2 = "\x1b[1;33m"; // ANSI escape for yellow
                var ogusr = Environment.GetEnvironmentVariable("USERNAME");
                string usr = removeNewLine(ogusr);
                var main = $"{color1}#ezpkg \x1b[0m{color2}<{usr}>\x1b[0m ~>";
                Console.Write(main);
                var ogcmd = Console.ReadLine();
                var cmd = ogcmd.ToLower();
                string[] cmdsplit = ogcmd.Split(' ');
                switch (cmdsplit[0])
                {
                    case "h":
                    case "help":
                        Console.WriteLine($"\x1b[1;33m        < --- help --- >\x1b[0m");
                        Console.WriteLine($"\x1b[31minstall - install a package \x1b[1;32m#ezpkg \x1b[0m\x1b[1;33m<{usr}>\x1b[0m ~> \x1b[31minstall <package>\x1b[33m");
                        Console.WriteLine($"\x1b[31muninstall - uninstall a package \x1b[1;32m#ezpkg \x1b[0m\x1b[1;33m<{usr}>\x1b[0m ~> \x1b[31muninstall(or rm or delete or remove) <package>\x1b[33m");
                        Console.WriteLine($"\x1b[31mlist - lists all packages \x1b[1;32m#ezpkg \x1b[0m\x1b[1;33m<{usr}>\x1b[0m ~> \x1b[31mlist(or ls)\x1b[33m");
                        Console.WriteLine($"\x1b[31mupdate - update all packages \x1b[1;32m#ezpkg \x1b[0m\x1b[1;33m<{usr}>\x1b[0m ~> \x1b[31mupdate\x1b[33m");
                        Console.WriteLine($"\x1b[1;33m        < --- help --- >\x1b[0m");
                        break;

                    case "install":
                        hiddenrun($"curl -O {ezpkgpath}\\temp https://example.com/{cmdsplit[1]}.zip");
                        // Install the file
                        hiddenrun($"Expand-Archive -Path {ezpkgpath}\\temp\\{cmdsplit[1]} -DestinationPath {ezpkgpath}\\packages");
                        break;

                    case "ls":
                    case "list":
                        // Check if the path contains files
                        string[] files = Directory.GetFiles($"{ezpkgpath}\\packages");

                        if (files.Length == 0) // Check if the array is empty
                        {
                            Console.WriteLine("\x1b[41mYou haven't installed anything yet?\x1b[0m");
                        }
                        else
                        {
                            foreach (string file in files)
                            {
                                Console.WriteLine(file);
                            }
                        }
                        break;

                    case "update":
                        // TODO: update logic here
                        // TODO: needs server-side logic (in Python or C# amazon s3 if possible)
                        // TODO: add json read/write (Newtonsoft.Json)
                        break;
                    case "uninstall":
                    case "rm":
                    case "remove":
                    case "delete":
                        var yesorno = AnsiConsole.Prompt(
    new SelectionPrompt<string>()
        .Title($"are you sure, you want to [red]delete {cmdsplit[1]}[/]?")
        .PageSize(3)
        .AddChoices(new[] {
                    "yes",
                    "no"
        }));
                        if (yesorno == "yes")
                        {
                            try
                            {
                                Directory.Delete($"{ezpkgpath}\\packages\\{cmdsplit[1]}", true);
                                Console.WriteLine($"{cmdsplit[1]} \u001b[31mhas been deleted\u001b[0m");
                            }
                            catch (DirectoryNotFoundException)
                            {
                                Console.WriteLine("\u001b[41mError: that package doesnt exist or not even installed!\x1b[0m");
                            }
                        }
                        else
                        {
                            Console.WriteLine("ok");
                        }
                        break;
                    default:
                        Console.WriteLine($"\u001b[1;33m{cmdsplit[0]} is not known command? try 'h' or 'help' ?\u001b[0m");
                        break;
                }
            }
        }
    }
}
