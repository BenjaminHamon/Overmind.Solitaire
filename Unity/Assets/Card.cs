using Overmind.Unity;
using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace Overmind.Solitaire.Unity
{
	public class Card : MonoBehaviour
	{
		[SerializeField]
		private new SpriteRenderer renderer;
		[SerializeField]
		private new Collider2D collider;
		[SerializeField]
		private Sprite frontSprite;
		[SerializeField]
		private Sprite backSprite;

		public Collider2D Collider { get { return collider; } }

		public Game Game;
		public CardPile Parent;

		private CardType type;
		[ExposeProperty]
		public CardType Type
		{
			get { return type; }
			set
			{
				if (type == value)
					return;
				type = value;
				UpdateSprite();
			}
		}

		private int number;
		[ExposeProperty]
		public int Number
		{
			get { return number; }
			set
			{
				if (number == value)
					return;
				number = value;
				UpdateSprite();
			}
		}

		private bool visible;
		[ExposeProperty]
		public bool Visible
		{
			get { return visible; }
			set
			{
				if (visible == value)
					return;
				visible = value;
				renderer.sprite = visible ? frontSprite : backSprite;
			}
		}

		private Transform draggingHandler;
		private Vector3 draggingStartingPoint;
		private Vector3 draggingOffset;

		private float lastClick;

		public void Start()
		{
			UpdateSprite();
		}

		private void UpdateSprite()
		{
			frontSprite = Resources.Load<Sprite>("Cards/Card" + type + number);
			renderer.sprite = visible ? frontSprite : backSprite;
		}

		public void OnMouseDown()
		{
			draggingStartingPoint = Camera.main.ScreenToWorldPoint(Input.mousePosition);
		}

		public void OnMouseDrag()
		{
			if (Visible == false)
				return;

			Vector3 newPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
			if (draggingHandler == null)
			{
				float dragDelta = ((Vector2)newPosition - (Vector2)draggingStartingPoint).magnitude;
				if (dragDelta > 0.1f)
					StartDragging();
			}

			if (draggingHandler != null)
			{
				newPosition += draggingOffset;
				newPosition.z = -5;
				draggingHandler.position = newPosition;
			}
		}

		public void OnMouseUp()
		{
			if (Time.time - lastClick > 0.5f)
			{
				lastClick = Time.time;
			}
			else
			{
				// Debug.Log("DoubleClick");

				if ((Parent is FoundationCardPile) == false)
				{
					foreach (FoundationCardPile foundationCardPile in Game.FoundationCardPiles)
					{
						if (foundationCardPile.TryPush(this))
							break;
					}
				}

				lastClick = 0;
			}

			if ((Visible == false) && (Parent.Peek() == this))
				Visible = true;

			if (draggingHandler != null)
				Drop();
		}

		private void StartDragging()
		{
			// Debug.Log("[Card] StartDragging");

			Vector3 initialPosition = transform.position;
			draggingOffset = initialPosition - Camera.main.ScreenToWorldPoint(Input.mousePosition);

			draggingHandler = new GameObject().transform;
			draggingHandler.name = "DraggingHandler";
			draggingHandler.position = initialPosition;

			transform.SetParent(draggingHandler);
			if (Parent is TableauCardPile)
			{
				foreach (Card card in ((TableauCardPile)Parent).GetChildren(this))
					card.transform.SetParent(draggingHandler);
			}
		}

		private void Drop()
		{
			// Debug.Log("[Card] Drop");

			List<Card> childCards = new List<Card>();
			if (Parent is TableauCardPile)
				childCards = ((TableauCardPile)Parent).GetChildren(this).ToList();

			bool moved = false;
			Bounds bounds = collider.bounds;
			// Debug.DrawLine(bounds.min, bounds.max, Color.red, 3);

			// Disable dragged card colliders to detect the collider under them
			collider.enabled = false;
			foreach (Card child in childCards)
				child.collider.enabled = false;

			Collider2D overCollider = Physics2D.OverlapArea(bounds.min, bounds.max);

			if (overCollider != null)
			{
				// Debug.Log("[Card] Drop on " + overCollider.name, overCollider);
				CardPile cardPile = overCollider.GetComponent<CardPile>();
				if (cardPile == null)
					cardPile = overCollider.GetComponentInParent<CardPile>();
				if (cardPile != null)
					moved = cardPile.TryPush(this);
			}

			collider.enabled = true;
			foreach (Card child in childCards)
				child.collider.enabled = true;

			if (moved == false)
			{
				transform.SetParent(Parent.transform, false);
				foreach (Card child in childCards)
					child.transform.SetParent(Parent.transform);
				Parent.ResetDepth();
			}

			Destroy(draggingHandler.gameObject);
		}

		public override string ToString()
		{
			return String.Format("Card {0} {1}", type, number);
		}
	}
}
