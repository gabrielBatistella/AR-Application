using UnityEngine;

public class FollowGyroscope : MonoBehaviour
{
    private void Start()
    {
        if (SystemInfo.supportsGyroscope)
        {
            Input.gyro.enabled = true;
        }
    }

    private void Update()
    {
        if (SystemInfo.supportsGyroscope)
        {
            transform.rotation = GyroToUnity(Input.gyro.attitude);
        }
    }

    private Quaternion GyroToUnity(Quaternion gyroQuat)
    {
        Quaternion unityQuat = new Quaternion(gyroQuat.x, gyroQuat.y, -gyroQuat.z, -gyroQuat.w);
        return unityQuat;
    }
}
