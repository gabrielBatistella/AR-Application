using UnityEngine;
using UnityEngine.UI;

public class TabsHandler : MonoBehaviour
{
    [SerializeField] private Image openTabButtonImage;
    [SerializeField] private Sprite openTabIcon;
    [SerializeField] private Sprite closeTabIcon;

    [SerializeField] private bool startOpen = false;

    private void Start()
    {
        if (startOpen)
        {
            OpenTab();
        }
        else
        {
            CloseTab();
        }
    }

    public void ToggleTab()
    {
        if (gameObject.activeSelf)
        {
            CloseTab();
        }
        else
        {
            OpenTab();
        }
    }

    private void OpenTab()
    {
        gameObject.SetActive(true);
        openTabButtonImage.sprite = closeTabIcon;
    }

    private void CloseTab()
    {
        gameObject.SetActive(false);
        openTabButtonImage.sprite = openTabIcon;
    }
}
