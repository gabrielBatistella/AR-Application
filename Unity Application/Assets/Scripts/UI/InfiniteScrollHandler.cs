using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(ScrollRect))]
public class InfiniteScrollHandler : MonoBehaviour
{
    [SerializeField] private RectTransform viewport;
    [SerializeField] private RectTransform contentPanel;
    [SerializeField] private VerticalLayoutGroup layoutGroup;

    [SerializeField] private List<RectTransform> itemList;

    private ScrollRect scrollRect;

    private float startingScrollPos;
    private Vector2 oldVelocity;
    private bool isUpdated;

    private void Awake()
    {
        scrollRect = GetComponent<ScrollRect>();
        oldVelocity = Vector2.zero;
        isUpdated = false;
    }

    private void Start()
    {
        int amountToAdd = Mathf.CeilToInt(viewport.rect.height / (itemList[0].rect.height + layoutGroup.spacing));
        startingScrollPos = (itemList[0].rect.height + layoutGroup.spacing) * amountToAdd - viewport.rect.height / 2 + itemList[0].rect.height / 2;

        for (int i = 0; i < amountToAdd; i++)
        {
            int idx = i % itemList.Count;

            RectTransform newItem = Instantiate(itemList[idx], contentPanel);
            newItem.SetAsLastSibling();
        }

        for (int i = 0; i < amountToAdd; i++)
        {
            int idx = (itemList.Count - 1 - i) % itemList.Count;
            if (idx < 0) idx += itemList.Count;

            RectTransform rectTransform = Instantiate(itemList[idx], contentPanel);
            rectTransform.SetAsFirstSibling();
        }

        SetScrollPosition(0f);
        //contentPanel.localPosition = new Vector3(contentPanel.localPosition.x, startingScrollPos, contentPanel.localPosition.z);
    }

    private void Update()
    {
        if (isUpdated)
        {
            isUpdated = false;
            scrollRect.velocity = oldVelocity;
        }

        /*
        if (contentPanel.localPosition.y < 0)
        {
            Canvas.ForceUpdateCanvases();
            oldVelocity = scrollRect.velocity;
            contentPanel.localPosition += new Vector3(0, (itemList[0].rect.height + layoutGroup.spacing) * itemList.Count, 0);
            isUpdated = true;
        }

        if (contentPanel.localPosition.y > (itemList[0].rect.height + layoutGroup.spacing) * itemList.Count)
        {
            Canvas.ForceUpdateCanvases();
            oldVelocity = scrollRect.velocity;
            contentPanel.localPosition -= new Vector3(0, (itemList[0].rect.height + layoutGroup.spacing) * itemList.Count, 0);
            isUpdated = true;
        }
        */

        for (int i = 0; i < contentPanel.childCount; i++)
        {
            float scrollPos = contentPanel.localPosition.y + contentPanel.GetChild(i).localPosition.y;
            contentPanel.GetChild(i).localScale = new Vector2(Mathf.Lerp(1f, 0.9f, Mathf.Abs(scrollPos + viewport.rect.height / 2) / (itemList[0].rect.height)), 1f);
        }
    }

    public void SetScrollPosition(float pos)
    {
        Canvas.ForceUpdateCanvases();
        oldVelocity = scrollRect.velocity;
        contentPanel.localPosition = new Vector3(contentPanel.localPosition.x, startingScrollPos + (itemList[0].rect.height + layoutGroup.spacing) * pos, contentPanel.localPosition.z);
        isUpdated = true;
    }
}