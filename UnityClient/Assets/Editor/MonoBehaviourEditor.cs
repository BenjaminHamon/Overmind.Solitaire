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
	public class MonoBehaviourEditor : UnityEditor.Editor
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
				PropertyField(property);
				EditorGUILayout.EndHorizontal();
			}

			EditorGUILayout.EndVertical();
		}

		private void PropertyField(PropertyInfo property)
		{
			// Beware about refactoring using object since comparison will break due to boxing

			string name = ObjectNames.NicifyVariableName(property.Name);

			if (property.PropertyType == typeof(bool))
			{
				bool oldValue = (bool)property.GetValue(target);
				bool newValue = EditorGUILayout.Toggle(name, oldValue);

				if (oldValue != newValue)
					TrySetPropertyValue(property, newValue);
			}
			else if (property.PropertyType == typeof(int))
			{
				int oldValue = (int)property.GetValue(target);
				int newValue = EditorGUILayout.IntField(name, oldValue);

				if (oldValue != newValue)
					TrySetPropertyValue(property, newValue);
			}
			else if (property.PropertyType == typeof(float))
			{
				float oldValue = (float)property.GetValue(target);
				float newValue = EditorGUILayout.FloatField(name, oldValue);

				if (oldValue != newValue)
					TrySetPropertyValue(property, newValue);
			}
			else if (property.PropertyType.IsEnum)
			{
				Enum oldValue = (Enum)property.GetValue(target);
				Enum newValue = EditorGUILayout.EnumPopup(name, oldValue);

				if (oldValue.Equals(newValue) == false)
					TrySetPropertyValue(property, newValue);
			}
			else if (property.PropertyType == typeof(string))
			{
				string oldValue = (string)property.GetValue(target);
				string newValue = EditorGUILayout.TextField(name, oldValue);

				if (oldValue != newValue)
					TrySetPropertyValue(property, newValue);
			}
			else if (property.PropertyType == typeof(Vector2))
			{
				Vector2 oldValue = (Vector2)property.GetValue(target);
				Vector2 newValue = EditorGUILayout.Vector2Field(name, oldValue);

				if (oldValue != newValue)
					TrySetPropertyValue(property, newValue);
			}
			else if (property.PropertyType == typeof(Vector3))
			{
				Vector3 oldValue = (Vector3)property.GetValue(target);
				Vector3 newValue = EditorGUILayout.Vector3Field(name, oldValue);

				if (oldValue != newValue)
					TrySetPropertyValue(property, newValue);
			}
			else if (typeof(UnityEngine.Object).IsAssignableFrom(property.PropertyType))
			{
				UnityEngine.Object oldValue = (UnityEngine.Object)property.GetValue(target);
				UnityEngine.Object newValue = EditorGUILayout.ObjectField(name, oldValue, property.PropertyType, EditorUtility.IsPersistent(target) == false);

				if (oldValue != newValue)
					TrySetPropertyValue(property, newValue);
			}
			else
			{
				throw new Exception(String.Format("Unsupported type '{0}'", property.PropertyType));
			}
		}

		private void TrySetPropertyValue(PropertyInfo property, object newValue)
		{
			try
			{
				property.SetValue(target, newValue);
			}
			catch (Exception exception)
			{
				UnityEngine.Debug.LogException(exception, target);
			}

			EditorUtility.SetDirty(target);
		}
	}
}
