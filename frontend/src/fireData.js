// fireData.js
import { getFirestore, doc, setDoc } from 'firebase/firestore';

const db = getFirestore();

/**
 * Updates intended major and/or community college for the logged-in user.
 * This is safe to call on every selection change.
 */
export const updateUserProfile = async (uid, { major, communityCollege }) => {
  if (!uid) {
    console.error('[fireData] Missing uid');
    return;
  }

  const updates = {};
  if (major !== undefined) updates.major = major;
  if (communityCollege !== undefined) updates.communityCollege = communityCollege;

  if (Object.keys(updates).length === 0) return;

  try {
    const ref = doc(db, 'userInformation', uid);
    await setDoc(ref, updates, { merge: true });
    console.log('[fireData] Profile updated:', updates);
  } catch (err) {
    console.error('[fireData] Update failed:', err);
  }
};

export const fetchUserProfile = async (uid) => {
  if (!uid) return null;

  try {
    const ref = doc(db, 'userInformation', uid);
    const snap = await getDoc(ref);

    if (snap.exists()) {
      return snap.data();
    }
  } catch (err) {
    console.error('[fireData] Fetch failed:', err);
  }

  return null;
};