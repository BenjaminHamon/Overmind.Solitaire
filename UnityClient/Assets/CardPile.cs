using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace Overmind.Solitaire.Unity
{
	public class CardPile : MonoBehaviour
	{
		protected Stack<Card> Cards = new Stack<Card>();

		public Card Peek()
		{
			return Cards.FirstOrDefault();
		}

		public void Push(Card card)
		{
			// Debug.Log("[CardPile] Push " + card + " to " + this, this);

			if (card.Parent == null)
			{
				DoPush(card);
			}
			else
			{
				IEnumerable<Card> poppedCardList = card.Parent.Pop(card);
				foreach (Card poppedCard in poppedCardList.Reverse())
					DoPush(poppedCard);
			}
		}

		protected virtual void DoPush(Card card)
		{
			Vector3 cardPosition = Vector3.zero;
			Card topCard = Cards.FirstOrDefault();
			if (topCard != null)
				cardPosition = topCard.transform.localPosition;
			cardPosition.z -= 0.1f;
			card.transform.localPosition = cardPosition;

			card.transform.SetParent(transform, false);
			card.Parent = this;
			Cards.Push(card);
		}

		public IEnumerable<Card> Pop(Card card)
		{
			List<Card> poppedCards = new List<Card>();
			while (Cards.Peek() != card)
				poppedCards.Add(Cards.Pop());
			poppedCards.Add(Cards.Pop());
			return poppedCards;
		}

		public virtual bool TryPush(Card card)
		{
			return false;
		}

		public void ResetDepth()
		{
			float z = -0.1f * Cards.Count;

			foreach (Card card in Cards)
			{
				Vector3 cardPosition = card.transform.localPosition;
				cardPosition.z = z;
				card.transform.localPosition = cardPosition;
				z += 0.1f;
			}
		}
	}
}
