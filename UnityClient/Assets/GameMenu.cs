using System;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace Overmind.Solitaire.UnityClient
{
	public class GameMenu : MonoBehaviour
	{
		[SerializeField]
		private InputField seedInput;
		[SerializeField]
		private Button lastSeedButton;
		[SerializeField]
		private bool randomSeedOnStart;

		private int seed
		{
			get { return Int32.Parse(seedInput.text); }
			set { seedInput.text = value.ToString(); }
		}

		public void Start()
		{
			if (randomSeedOnStart)
				SetRandomSeed();
			if (Application.GameSeed != null)
				lastSeedButton.interactable = true;
		}

		public void Update()
		{
			if (Input.GetKeyDown(KeyCode.Escape))
				Exit();
		}

		public void StartNewGame()
		{
			Application.GameSeed = seed;
			SceneManager.LoadScene("GameScene");
		}

		public void SetRandomSeed()
		{
			System.Random random = new System.Random();
			seed = random.Next();
		}

		public void SetLastSeed()
		{
			seed = Application.GameSeed.Value;
		}

		public void Exit()
		{
			Debug.Log("[GameMenu] Exit");
			UnityEngine.Application.Quit();
		}
	}
}
