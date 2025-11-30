import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useMutation, useQuery } from "@apollo/client";
import {
  GET_ME,
  LOGIN_USER,
  LOGOUT_USER,
  REGISTER_USER,
} from "../graphql/queries";
import { AuthUser, LoginInput, RegisterInput } from "../types";

interface AuthContextType {
  user: AuthUser | null;
  loading: boolean;
  login: (input: LoginInput) => Promise<{ success: boolean; message: string }>;
  register: (
    input: RegisterInput
  ) => Promise<{ success: boolean; message: string }>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  const { refetch: refetchMe } = useQuery(GET_ME, {
    skip: true,
    onError: (error) => {
      console.log("GraphQL GET_ME error (expected on first load):", error.message);
      setLoading(false);
    },
  });

  const [loginMutation] = useMutation(LOGIN_USER);
  const [registerMutation] = useMutation(REGISTER_USER);
  const [logoutMutation] = useMutation(LOGOUT_USER);

  // Check if user is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data } = await refetchMe();
        if (data?.me) {
          setUser(data.me);
        }
      } catch (error) {
        console.log("Not authenticated");
      } finally {
        setLoading(false);
      }
    };
    checkAuth();
  }, [refetchMe]);

  const login = async (input: LoginInput) => {
    try {
      const { data } = await loginMutation({ variables: { input } });
      if (data?.loginUser?.success) {
        setUser(data.loginUser.user);
        return { success: true, message: data.loginUser.message };
      }
      return {
        success: false,
        message: data?.loginUser?.message || "Login failed",
      };
    } catch (error: any) {
      return { success: false, message: error.message || "Login error" };
    }
  };

  const register = async (input: RegisterInput) => {
    try {
      const { data } = await registerMutation({ variables: { input } });
      if (data?.registerUser?.success) {
        return { success: true, message: data.registerUser.message };
      }
      return {
        success: false,
        message: data?.registerUser?.message || "Registration failed",
      };
    } catch (error: any) {
      return { success: false, message: error.message || "Registration error" };
    }
  };

  const logout = async () => {
    try {
      await logoutMutation();
      setUser(null);
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
