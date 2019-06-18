using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Editor
{
	/// <summary>Inspector to expose a component properties with <see cref="ExposePropertyAttribute"/>.</summary>
	/// <see href="http://wiki.unity3d.com/index.php/ExposePropertiesInInspector_Generic"/>
	[CustomEditor(typeof(MonoBehaviour), true)]
	public class MonoBehaviourBaseEditor : UnityEditor.Editor
	{
		private ICollection<PropertyInfo> propertyCollection;

		public virtual void OnEnable()
		{
			propertyCollection = target.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance)
				.Where(property => property.GetCustomAttributes(true).Any(attribute => attribute is ExposePropertyAttribute))
				.ToList();
		}

		public override void OnInspectorGUI()
		{
			DrawDefaultInspector();

			EditorGUILayout.BeginVertical();
			foreach (PropertyInfo property in propertyCollection)
			{
				EditorGUILayout.BeginHorizontal();
				string name = ObjectNames.NicifyVariableName(property.Name);
				object oldValue = property.GetValue(target, null);
				object newValue;

				if (property.PropertyType == typeof(bool))
					newValue = EditorGUILayout.Toggle(name, (bool)oldValue);
				else if (property.PropertyType == typeof(int))
					newValue = EditorGUILayout.IntField(name, (int)oldValue);
				else if (property.PropertyType == typeof(float))
					newValue = EditorGUILayout.FloatField(name, (float)oldValue);
				else if (property.PropertyType.IsEnum)
					newValue = EditorGUILayout.EnumPopup(name, (Enum)oldValue);
				else if (property.PropertyType == typeof(string))
					newValue = EditorGUILayout.TextField(name, (string)oldValue);
				else if (property.PropertyType == typeof(Vector2))
					newValue = EditorGUILayout.Vector2Field(name, (Vector2)oldValue);
				else if (property.PropertyType == typeof(Vector3))
					newValue = EditorGUILayout.Vector3Field(name, (Vector3)oldValue);
				else if (typeof(UnityEngine.Object).IsAssignableFrom(property.PropertyType))
					newValue = EditorGUILayout.ObjectField(name, (UnityEngine.Object)oldValue, property.PropertyType, EditorUtility.IsPersistent(target) == false);
				else
					throw new Exception("[MonoBehaviourEditor.OnInspectorGUI] Unhandled type " + property.PropertyType + " for property " + property.Name);

				try { property.SetValue(target, newValue, null); }
				catch (Exception exception) { UnityEngine.Debug.LogError(exception, target); }
				EditorUtility.SetDirty(target);

				EditorGUILayout.EndHorizontal();
			}
			EditorGUILayout.EndVertical();
		}
	}
}
