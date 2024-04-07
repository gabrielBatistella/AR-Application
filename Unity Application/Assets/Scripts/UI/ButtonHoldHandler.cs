using System.Collections;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.EventSystems;
using UnityEngine.UI;

[RequireComponent(typeof(Button))]
public class ButtonHoldHandler : MonoBehaviour, IPointerDownHandler, IPointerUpHandler, IPointerEnterHandler, IPointerExitHandler
{
    [SerializeField] private UnityEvent onPointerDown;
    [SerializeField] private UnityEvent onPointerUp;
    [SerializeField] private UnityEvent whilePointerPressed;

    private Button button;

    private void Awake()
    {
        button = GetComponent<Button>();
    }

    private IEnumerator WhilePressed()
    {
        while (true)
        {
            whilePointerPressed?.Invoke();
            yield return null;
        }
    }

    public void OnPointerDown(PointerEventData eventData)
    {
        if (button.interactable)
        {
            StopAllCoroutines();
            StartCoroutine(nameof(WhilePressed));

            onPointerDown?.Invoke();
        }
    }

    public void OnPointerUp(PointerEventData eventData)
    {
        StopAllCoroutines();
        onPointerUp?.Invoke();
    }

    public void OnPointerEnter(PointerEventData eventData)
    {

    }

    public void OnPointerExit(PointerEventData eventData)
    {
        StopAllCoroutines();
        onPointerUp?.Invoke();
    }
}
