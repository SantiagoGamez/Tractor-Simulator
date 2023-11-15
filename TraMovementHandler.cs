// Tractor movement handler
// JSON data format:
// {"X_COORDINATE": 0.0, "Z_COORDINATE": 0.0 }


using UnityEngine;
using System;

[Serializable]
public class PositionData
{
    public float X_COORDINATE;
    public float Z_COORDINATE;
}

public class TraMovementHandler : MonoBehaviour
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

        // Calculate the direction of movement
        Vector3 direction = (targetPosition - transform.position).normalized;

        if (direction != Vector3.zero)
        {
            Quaternion toRotation = Quaternion.LookRotation(direction, Vector3.up);
            transform.rotation = Quaternion.RotateTowards(transform.rotation, toRotation, 10);
        }

        // Move the object smoothly to the target position
        transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime);



    }

    void UpdateTargetPosition()
    {
        PositionData data = JsonUtility.FromJson<PositionData>(jsonText);
        Vector3 targetPositionXZ = new Vector3(data.X_COORDINATE, 0, data.Z_COORDINATE);

        // Cast a ray downwards from the target XZ position
        RaycastHit hit;
        if (Physics.Raycast(targetPositionXZ + Vector3.up * 1000, Vector3.down, out hit))
        {
            // If the ray hits the terrain, set the target position to the hit point
            targetPosition = hit.point;
        }
        else
        {
            // If the ray does not hit the terrain, keep the current Y position
            targetPosition = new Vector3(data.X_COORDINATE, transform.position.y, data.Z_COORDINATE);
        }
    }

}