using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Overmind.Solitaire.UnityClient
{
	public class Game : MonoBehaviour
	{
		[SerializeField]
		private GameObject foundationPilePrefab = null;
		[SerializeField]
		private GameObject tableauPilePrefab = null;
		[SerializeField]
		private GameObject cardPrefab = null;

		[SerializeField]
		private StockCardPile stock = null;
		[SerializeField]
		private Transform foundation = null;
		[SerializeField]
		private Transform tableau = null;
		[SerializeField]
		private GameObject victory = null;

		[SerializeField]
		private GameConfiguration Configuration = null;
		[SerializeField]
		private int Seed = 0;

		private System.Random random;
		private List<FoundationCardPile> foundationCardPiles = new List<FoundationCardPile>();
		public IEnumerable<FoundationCardPile> FoundationCardPiles { get { return foundationCardPiles; } }

		public void Start()
		{
			if (Application.GameSeed != null)
				Seed = Application.GameSeed.Value;
			Debug.Log(String.Format("[Game] Starting (Seed: {0})", Seed));
			random = new System.Random(Seed);

			Stack<Card> cardStack = new Stack<Card>(CreateDeck());

			for (int foundationPileIndex = 0; foundationPileIndex < Configuration.CardTypes.Count; foundationPileIndex++)
				CreateFoundationPile();

			foreach (int pileCardSize in Configuration.Tableau)
			{
				TableauCardPile tableauPile = CreateTableauPile();
				for (int pileCardIndex = 0; pileCardIndex < pileCardSize; pileCardIndex++)
					tableauPile.Push(cardStack.Pop());
				Card topCard = tableauPile.Peek();
				if (topCard != null)
					topCard.Visible = true;
			}

			foreach (Card card in cardStack)
				stock.Push(card);
		}

		public void Update()
		{
			if (Input.GetKeyDown(KeyCode.Escape))
				Exit();
		}

		public void OnDestroy()
		{
			foreach (FoundationCardPile foundationPile in foundationCardPiles)
				foundationPile.Completed -= CheckVictory;
		}

		private List<Card> CreateDeck()
		{
			List<Card> cardDeck = new List<Card>();
			foreach (CardType cardType in Configuration.CardTypes)
			{
				for (int cardNumber = 1; cardNumber <= Configuration.CardMaxNumber; cardNumber++)
				{
					cardDeck.Add(CreateCard(cardType, cardNumber));
				}
			}

			cardDeck = cardDeck.OrderBy(c => random.Next()).ToList();
			return cardDeck;
		}

		private Card CreateCard(CardType type, int number)
		{
			GameObject cardObject = Instantiate(cardPrefab);
			cardObject.transform.SetParent(transform);
			cardObject.SetActive(false);

			Card card = cardObject.GetComponent<Card>();
			card.Game = this;
			card.Type = type;
			card.Number = number;
			card.Visible = false;
			card.name = card.ToString();

			cardObject.SetActive(true);

			return card;
		}

		private FoundationCardPile CreateFoundationPile()
		{
			FoundationCardPile foundationPile = Instantiate(foundationPilePrefab).GetComponent<FoundationCardPile>();
			foundationPile.CardMaxNumber = Configuration.CardMaxNumber;
			foundationPile.Completed += CheckVictory;
			foundationPile.transform.SetParent(foundation);
			foundationCardPiles.Add(foundationPile);
			return foundationPile;
		}

		private TableauCardPile CreateTableauPile()
		{
			TableauCardPile tableauPile = Instantiate(tableauPilePrefab).GetComponent<TableauCardPile>();
			tableauPile.CardMaxNumber = Configuration.CardMaxNumber;
			tableauPile.transform.SetParent(tableau);
			return tableauPile;
		}

		private void CheckVictory()
		{
			// Debug.Log("[Game] Checking victory");

			if (foundationCardPiles.All(cardPile => cardPile.IsComplete))
			{
				Debug.Log("[Game] Victory");
				StartCoroutine(ShowVictory());
			}
		}

		private IEnumerator ShowVictory()
		{
			victory.SetActive(true);
			yield return new WaitForSeconds(2);
			Exit();
		}

		private void Exit()
		{
			Debug.Log("[Game] Exit");
			SceneManager.LoadScene("MenuScene");
		}
	}
}
