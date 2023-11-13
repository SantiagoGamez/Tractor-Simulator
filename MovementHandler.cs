using UnityEngine;
using System;

[Serializable]
public class PositionData
{
    public float X_COORDINATE;
    public float Y_COORDINATE;
    public float Z_COORDINATE;
}

public class MovementHandler : MonoBehaviour
{
    public string jsonText;
    private string lastJsonText;
    private Vector3 targetPosition;

    void Start()
    {
        lastJsonText = jsonText;
        UpdateTargetPosition();
    }

    void Update()
    {
        if (jsonText != lastJsonText)
        {
            lastJsonText = jsonText;
            UpdateTargetPosition();
        }

        // Move the object smoothly to the target position
        transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime);

        if (targetPosition != Vector3.zero)
        {
            transform.forward = targetPosition;
        }

    }

    void UpdateTargetPosition()
    {
        PositionData data = JsonUtility.FromJson<PositionData>(jsonText);
        targetPosition = new Vector3(data.X_COORDINATE, data.Y_COORDINATE, data.Z_COORDINATE);
    }
}
