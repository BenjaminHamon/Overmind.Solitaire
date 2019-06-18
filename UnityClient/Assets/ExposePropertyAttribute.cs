using System;

namespace Overmind.Solitaire.UnityClient
{
	/// <summary>Attribute for a property to be exposed in the inspector.</summary>
	/// <see href="http://wiki.unity3d.com/index.php/ExposePropertiesInInspector_Generic"/>
	[AttributeUsage(AttributeTargets.Property)]
	public class ExposePropertyAttribute : Attribute
	{ }
}
