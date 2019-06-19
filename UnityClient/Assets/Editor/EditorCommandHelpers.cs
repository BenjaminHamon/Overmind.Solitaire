using System;
using System.Collections.Generic;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class EditorCommandHelpers
	{
		public static void ConfigureLogging()
		{
			UnityEngine.Application.SetStackTraceLogType(LogType.Log, StackTraceLogType.None);
		}

		public static Dictionary<string, string> FindMethodArguments()
		{
			IList<string> rawArguments = Environment.GetCommandLineArgs();
			Dictionary<string, string> methodArguments = new Dictionary<string, string>();

			bool isSelectingArguments = false;

			foreach (string argument in rawArguments)
			{
				if (argument.StartsWith("-"))
				{
					isSelectingArguments = argument == "-executeMethodArguments";
				}
				else
				{
					if (isSelectingArguments)
					{
						IList<string> keyValuePair = argument.Split(new string[] { "=" }, StringSplitOptions.RemoveEmptyEntries);
						if (keyValuePair.Count != 2)
							throw new ArgumentException(String.Format("Invalid argument: '{0}'", argument));
						methodArguments.Add(keyValuePair[0], keyValuePair[1]);
					}
				}
			}

			return methodArguments;
		}

		public static TValue ParseArgument<TValue>(Dictionary<string, string> arguments, string key)
		{
			if (arguments.ContainsKey(key) == false)
				throw new ArgumentException(String.Format("Missing argument: '{0}'", key));
			return (TValue) Convert.ChangeType(arguments[key], typeof(TValue));
		}
	}
}
